import { responseParser } from 'servequery-ui-lib/api/client-heplers'
import { ServiceHeader } from 'servequery-ui-lib/components/ServiceHeader'
import { BreadCrumbs } from 'servequery-ui-lib/router-utils/components/breadcrumbs'
import {
  FetchersProgress,
  NavigationProgress
} from 'servequery-ui-lib/router-utils/components/navigation-progress'
import { useCrumbsFromHandle, useCurrentRouteParams } from 'servequery-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'servequery-ui-lib/router-utils/router-builder'
import { Box, Stack } from 'servequery-ui-lib/shared-dependencies/mui-material'
import { Outlet, ScrollRestoration } from 'servequery-ui-lib/shared-dependencies/react-router-dom'
import { clientAPI } from '~/api'
import type { GetRouteByPath } from '~/routes/types'
import { HomeLink } from './components'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>

const crumb: CrumbDefinition = { title: 'Home' }

export const handle = { crumb }

export const loadData = () => clientAPI.GET('/api/version').then(responseParser())

export const Component = () => {
  const { loaderData } = useCurrentRouteParams<CurrentRoute>()
  const { crumbs } = useCrumbsFromHandle()

  return (
    <>
      <NavigationProgress />
      <ScrollRestoration />
      <ServiceHeader version={loaderData.version} HomeLink={HomeLink} />
      <Box p={3}>
        <Stack direction={'row'} alignItems={'center'} gap={2}>
          <BreadCrumbs crumbs={crumbs} />
          <FetchersProgress />
        </Stack>
        <Outlet />
      </Box>
    </>
  )
}
