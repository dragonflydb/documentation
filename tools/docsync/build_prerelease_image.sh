#!/usr/bin/env bash
# Build the Dragonfly production image for a tag whose GitHub release is still
# a draft, so the docsync scripts can run before the release is published.
#
# Upstream only pushes docker.dragonflydb.io/dragonflydb/dragonfly:<tag> when the
# release is published (.github/workflows/docker-release2.yml). Until then this
# script replicates that workflow's build locally: same draft release asset,
# same tools/packaging/Dockerfile.ubuntu-prod, same image name. The binary in the
# image is byte-identical to the release asset (checked below).
#
# The image stays local. Never `docker push` it: it carries the official image name.
# Everything here only reads from GitHub (gh api / gh release download).
#
# Run every docsync script with --skip-pull while the image only exists locally.
# Draft tags can move: re-run this script whenever the tag's commit changes (the
# scripts detect that and stop with "image ... was built from X, but tag ...
# points to Y upstream" or "inputs are from different commits").
#
#   tools/docsync/build_prerelease_image.sh v2.0.0               # host arch
#   tools/docsync/build_prerelease_image.sh v2.0.0 linux/amd64
set -euo pipefail

TAG=${1:?usage: $0 <tag> [platform]}
PLATFORM=${2:-linux/$(docker info --format '{{.Architecture}}' | sed 's/aarch64/arm64/;s/x86_64/amd64/')}
REPO=dragonflydb/dragonfly
IMAGE=docker.dragonflydb.io/dragonflydb/dragonfly:${TAG}
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

SHA=$(gh api "repos/$REPO/commits/$TAG" --jq .sha)
echo "tag $TAG -> $SHA, platform $PLATFORM"

if docker manifest inspect "$IMAGE" >/dev/null 2>&1; then
  echo "NOTE: $IMAGE is published; use 'docker pull' and drop --skip-pull instead." >&2
fi

mkdir -p "$WORK/tools/docker" "$WORK/tools/packaging" "$WORK/releases"
for f in tools/docker/fetch_release.sh tools/docker/entrypoint.sh tools/docker/healthcheck.sh \
         tools/packaging/Dockerfile.ubuntu-prod; do
  gh api "repos/$REPO/contents/$f?ref=$SHA" --jq .content | base64 -d > "$WORK/$f"
done
chmod +x "$WORK"/tools/docker/*.sh

# The workflow fetches "dragonfly-.*\.tar\.gz", but the *-dbgsym tarballs unpack
# to a plain "dragonfly" that "COPY releases/dragonfly-*" never picks up.
gh release download "$TAG" -R "$REPO" -D "$WORK/releases" \
  -p 'dragonfly-aarch64.tar.gz' -p 'dragonfly-x86_64.tar.gz'
for f in "$WORK"/releases/*.tar.gz; do tar xfz "$f" -C "$WORK/releases"; done
rm "$WORK"/releases/*.tar.gz

docker build --platform "$PLATFORM" -f "$WORK/tools/packaging/Dockerfile.ubuntu-prod" \
  --label org.opencontainers.image.vendor="DragonflyDB LTD" \
  --label org.opencontainers.image.title="Dragonfly Production Image" \
  --label org.opencontainers.image.description="The fastest in-memory store" \
  --label org.opencontainers.image.version="$TAG" \
  --label org.opencontainers.image.revision="$SHA" \
  --label io.dragonflydb.local-build.source=draft-release-assets \
  -t "$IMAGE" "$WORK"

arch=$([ "$PLATFORM" = linux/amd64 ] && echo x86_64 || echo aarch64)
want=$(sha256sum "$WORK/releases/dragonfly-$arch" | cut -c1-64)
got=$(docker run --rm --pull=never --platform "$PLATFORM" --entrypoint sha256sum "$IMAGE" \
  /usr/local/bin/dragonfly | cut -c1-64)
[ "$want" = "$got" ] || { echo "binary mismatch: asset $want, image $got" >&2; exit 1; }

version=$(docker run --rm --pull=never --platform "$PLATFORM" --entrypoint dragonfly "$IMAGE" \
  --version | head -1 | sed 's/\x1b\[[0-9;]*m//g')
case "$version" in
  *"-$SHA"*) ;;
  *) echo "release asset is not built from $SHA: $version (assets not rebuilt yet after a tag move?)" >&2
     exit 1 ;;
esac
echo "OK: $IMAGE — $version (binary sha256 $got == release asset)"
