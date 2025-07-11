import type { CrumbDefinition } from 'servequery-ui-lib/router-utils/router-builder'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/reports'

const crumb: CrumbDefinition = { title: 'Reports' }

export const handle = { crumb }
