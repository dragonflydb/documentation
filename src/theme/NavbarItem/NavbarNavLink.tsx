import React, { useEffect, useState } from "react";
import NavbarNavLink from "@theme-original/NavbarItem/NavbarNavLink";
import type NavbarNavLinkType from "@theme/NavbarItem/NavbarNavLink";

type Props = React.ComponentProps<typeof NavbarNavLinkType>;

export default function NavbarNavLinkWrapper(props: Props): JSX.Element {
  const [githubStars, setGithubStars] = useState<number | null>(null);

  const isGithubStars = props.className.includes("nav-github-stars");

  useEffect(() => {
    if (!isGithubStars) return;

    const storedStars = +sessionStorage.getItem("GITHUB_STARS");

    if (storedStars) {
      return setGithubStars(storedStars);
    }

    const doEffect = async () => {
      const response = await fetch(
        "https://api.github.com/repos/dragonflydb/dragonfly"
      );
      const body = await response.json();
      const startsCount = body.stargazers_count as number;

      setGithubStars(startsCount);
      sessionStorage.setItem("GITHUB_STARS", String(startsCount));
    };

    doEffect();
  }, [, isGithubStars]);

  if (isGithubStars) {
    return (
      <NavbarNavLink
        {...props}
        style={
          isGithubStars && githubStars
            ? { opacity: 1, visibility: "visible" }
            : undefined
        }
        label={
          githubStars
            ? `${githubStars
                .toLocaleString("en-US", {
                  notation: "compact",
                  maximumFractionDigits: 1,
                })
                .toLowerCase()} stars`
            : props.label
        }
      />
    );
  }

  return <NavbarNavLink {...props} />;
}
