import type { BackendPaths } from 'servequery-ui-lib/api/types/v2'
import { createClient } from 'servequery-ui-lib/shared-dependencies/openapi-fetch'

export const clientAPI = createClient<BackendPaths>({ baseUrl: '/' })
