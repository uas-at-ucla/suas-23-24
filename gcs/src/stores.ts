import { writable } from 'svelte/store';
import type { LocationUpdatePayload } from './types';

export const dataStore = writable<LocationUpdatePayload>({});
