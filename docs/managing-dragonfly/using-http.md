# HTTP

Dragonfly supports HTTP for certain operations. By default, `HTTP` can be accessed on 
the same port as the main `TCP` port. However, this can be turned off by the command
`--primary_port_http_enabled=false`. Moreover, if `--admin_port` flag is set it also
supports `HTTP` on admin port.

# Authentication
By default, HTTP does not require authentication. However, if `requirepass` is set then
the HTTP request should authorize with username `default` and password the value
set with `requirepass`.

Note that `default` should not be confused with the ACL's `default` user. 
These two, do not always share the exact same password even if `requirepass` sets 
the `default` ACL user password because the vice versa is not true, that is, 
`ACL SETUSER default >newpass` will not change the current password specified in `requirepass`.

Also, if `admin_nopass` is set, it bypasses the `requirepass` option on admin port, allowing
all requests to that port without any authentication.

# Metrics page

Keep in mind that the `/metrics` page always bypasses auth. That means, that a user can freely
request that page without any auth validation.
