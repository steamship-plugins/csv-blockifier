# Deploying

This repository auto-deploys to Steamship when new versions are pushed.

* Pushing to `main` deploys to your production account on `api.steamship.com`
* Pushing to `vA.B.C` deploys to your production account on `api.steamship.com`
* Pushing to `staging` deploys to your staging account (if configured)

That deployment is parameterized by the following information:

* The `handle` property of `steamship.json`
* The `version` property of `steamship.json`
* The `STEAMSHIP_KEY` GitHub repository secret
* The `STEAMSHIP_API_BASE` GitHub repository secret (optional)
* The `STEAMSHIP_KEY_STAGING` GitHub repository secret
* The `STEAMSHIP_API_BASE_STAGING` GitHub repository secret (optional)

With this automated deployment flow, the version released to Steamship will be auto-flagged as the default version regardless of the version handle! New instances of your app or plugin will default to it unless a specific version was explicitly requested during their instantiation.

## Staging Strategy

If you fork this repository and would like to establish your own staging workflow, we suggest the following workflow:

1. Creating a second Steamship account to act as your staging account. For example `acme_staging`, if your account is `acme`
2. Set the `STEAMSHIP_KEY_STAGING` GitHub secret to the API Key of that account
3. Leave the `STEAMSHIP_API_BASE_STAGING` GitHub secret blank; it will default to the appropriate API endpoint.

## Troubleshooting

### The deployment fails because the version already exists

This means the version specified in `steamship.json` has already been registered with Steamship. Simply update the version in `steamship.json` to an identifier that has not yet been used.

### The deployment fails because the tag does not match the manifest file

This means you have tried to push a branch with a semver-style tag (like `v1.2.3`), resulting in a version deployment whose name must match that tag without the `v` prefix (`1.2.3`). Make sure the version field of `steamship.json` matches this string.

For example, if you are deploying branch `v6.0.0`, the `version` field of your `steamship.json` file must be `6.0.0`
