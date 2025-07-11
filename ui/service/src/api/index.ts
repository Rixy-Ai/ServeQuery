import type { BackendPaths } from 'servequery-ui-lib/api/types'
import { createClient } from 'servequery-ui-lib/shared-dependencies/openapi-fetch'

export const clientAPI = createClient<BackendPaths>({ baseUrl: '/' })
