import { rm } from 'node:fs/promises';

// Call only after Chrome exits, with this gate's own mkdtemp directory.
// A late profile write can race recursive removal. Bound retries; never hide
// persistent cleanup failures (force only tolerates an already absent path).
export async function removeBrowserProfile(profile) {
  await rm(profile, { recursive: true, force: true, maxRetries: 3, retryDelay: 100 });
}
