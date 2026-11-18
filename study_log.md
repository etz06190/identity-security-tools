# Week 1 (November 2026): tokens, claims and the two flows

What is a token

A token is issued by an authorization server after a successful authentication. It is a signed statement of authorization, created by the authorization server and checked by the resource server.

It is made of three parts, separated by dots in its encoded form: the header, which gives the token type, the algorithm used to create the signature and the ID of the key that signed it; the payload, which contains the claims; and the signature.

The issuer signs the token with its own private key. The checker verifies the signature with the matching public key, which the issuer publishes, and uses the key ID (kid) in the header to know which public key to use. A valid signature proves that the token came from that issuer and lets the checker detect any tampering. The checker also verifies that the issuer is one it trusts, that it is itself the intended audience, and that the token has not expired.

A token is valid for a limited time (3,600 seconds in my case). This short lifetime is a security mechanism for two reasons. First, the checker has no way to verify the identity of whoever presents the token: anyone who presents it is granted the rights it represents, which is why it is called a bearer token. A stolen token therefore works for the thief until it expires. Second, if the authorization is revoked at the issuer, the checker has no way of knowing, because it only examines the token itself.

The content of a token is not hidden. It is base64url encoded, not encrypted, and can easily be decoded, so it must never contain a password or any other secret. The token itself, however, must be stored and handled as securely as a password. 


What the claims mean

Who issued this token?
Delegated flow: "iss": "https://sts.windows.net/<tenant-id>/"
App-only flow: "iss": "https://sts.windows.net/<tenant-id>/"
In both flows this is answered by the iss (issuer) claim. It identifies the authorization server, and the tenant, that issued the token. The checker compares it with the issuer it trusts.

Who is it meant for?
Delegated flow: "aud": "00000003-0000-0000-c000-000000000000"
App-only flow: "aud": "https://graph.microsoft.com"
This is answered by the aud (audience) claim, which names the resource the token is intended for. The two values look different but both refer to Microsoft Graph: the first is Graph’s application ID and the second is its address. A resource server accepts a token only if the audience is itself.

When is it valid?
Three claims answer this: iat (issued at), nbf (not before) and exp (expiry). Each is a point in time, written as the number of seconds since January 1, 1970 (UTC). The token is valid from nbf until exp. Subtracting iat from exp gives the lifetime, which was about one hour for both of my tokens.

Who or what is it about?
The delegated token carries several claims that describe the user, such as "name": "alice.lab" and "upn": "alice.lab@<lab-tenant>.onmicrosoft.com", along with her object ID in oid.
The app-only token describes no person. It identifies the application through "oid": "3b94…" (the object ID of its service principal) and "app_displayname": "graph-lab-clientcred".

What is it allowed to do?
Delegated flow: "scp": "openid profile User.Read email"
App-only flow: "roles": ["User.Read.All"]
Each flow uses its own claim. In the delegated flow the rights are in scp (scope). Here the application may sign the user in and read that user’s own profile and email address. In the app-only flow the rights are in roles. Here the application may read the profile of every user in the tenant.

How the two flows differ

Who proves their identity, and with what?
In the delegated flow, the user proves her identity with a password. The token records this in "amr": ["pwd"].
In the app-only flow, the application proves its own identity with its application ID and its client secret.

Is a human present? Is a browser involved?
A human and a browser are involved in the delegated flow. Neither is involved in the app-only flow.

Which claims appear in one token and not the other?
scp, name and upn appear only in the delegated token.
roles and idp appear only in the app-only token.

How are the permissions expressed, and who granted them?
In the delegated flow, permissions are expressed in scp and were granted by the user herself, who consented when she signed in.
In the app-only flow, permissions are expressed in roles and were granted by an administrator. An application cannot grant permissions to itself.

What can a thief do with each kind of stolen token, and for how long?
A thief could do more damage with the app-only token, because it gives read access to every user in the tenant’s directory. That is valuable reconnaissance against the organization. The delegated token is limited to one user’s data, so the impact is smaller. In both cases the token works until it expires, about an hour after it was issued.

The delegated flow is used when a person is present at the screen. The app-only flow is used for automations that run in the background.

A stolen token is only useful for about an hour, so the more serious theft in each flow is the credential that can obtain new ones. In the app-only flow that is the client secret. A thief who has it can request new access tokens as the application until an administrator deletes or replaces the secret, or until the secret reaches its own expiry date, which can be months or years away. In the delegated flow it is the refresh token, which lets the client obtain new access tokens and lives much longer than they do. It stops working when the user’s password is changed, when an administrator revokes the user’s sessions, when the account is disabled, or when the user removes the application’s access. In both cases, an access token that was already issued keeps working until it expires. The difference is that ordinary events such as a password change cut off a stolen refresh token, while nothing interrupts a stolen client secret except someone deliberately removing it.



