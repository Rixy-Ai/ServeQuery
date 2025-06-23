import { JSONParseExtended } from 'servequery-ui-lib/api/JsonParser.ts'
import { responseParser } from 'servequery-ui-lib/api/client-heplers.ts'
import type { DashboardModel } from 'servequery-ui-lib/api/types/v2'
import { DrawDashboardPanels } from 'servequery-ui-lib/components/v2/Dashboard/HelperComponents/DrawDashboardPanels'
import { DashboardViewParamsContext } from 'servequery-ui-lib/contexts/DashboardViewParamsV2'
import { useCurrentRouteParams } from 'servequery-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'servequery-ui-lib/router-utils/router-builder'
import type { GetParams, loadDataArgs } from 'servequery-ui-lib/router-utils/types'
import { Box } from 'servequery-ui-lib/shared-dependencies/mui-material'
import { PanelComponent } from '~/Components/DashboardPanel'
import { OnClickedPointComponent } from '~/Components/GoToSnapshotButton'
import { clientAPI } from '~/api'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/?index'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type Params = GetParams<typeof currentRoutePath>

const crumb: CrumbDefinition = { title: 'Dashboard' }

export const handle = { crumb }

const loadDashboardAPI = '/api/v2/dashboards/{project_id}'
// type LoadDashboardAPIQuery = GetSearchParamsAPIs<'get'>[typeof loadDashboardAPI]

export const loadData = (
  { params, query }: loadDataArgs /* <{ queryKeys: keyof LoadDashboardAPIQuery }> */
) => {
  const { projectId } = params as Params

  return clientAPI
    .GET(loadDashboardAPI, { params: { path: { project_id: projectId }, query }, parseAs: 'text' })
    .then(responseParser())
    .then(JSONParseExtended<DashboardModel>)
}

export const Component = () => {
  const { loaderData: data } = useCurrentRouteParams<CurrentRoute>()

  return (
    <Box py={2}>
      <DashboardViewParamsContext.Provider value={{ OnClickedPointComponent }}>
        <DrawDashboardPanels PanelComponent={PanelComponent} panels={data.panels} />
      </DashboardViewParamsContext.Provider>
    </Box>
  )
}
