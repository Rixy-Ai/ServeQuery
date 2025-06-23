import type { CrumbDefinition } from 'servequery-ui-lib/router-utils/router-builder'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/test-suites'

const crumb: CrumbDefinition = { title: 'Test Suites' }

export const handle = { crumb }
