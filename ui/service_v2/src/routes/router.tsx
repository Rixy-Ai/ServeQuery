import {
  decorateAllRoutes,
  decorateTopLevelRoutes
} from 'servequery-ui-lib/router-utils/router-builder'
import { createBrowserRouter } from 'servequery-ui-lib/shared-dependencies/react-router-dom'
import { routes } from '~/routes/src'

const finalRoutes = routes.map((r) => decorateTopLevelRoutes(r)).map((r) => decorateAllRoutes(r))

export const router = createBrowserRouter(finalRoutes)
