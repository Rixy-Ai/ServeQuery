import React from 'react'
import ReactDOM from 'react-dom/client'

import type { AdditionalGraphInfo } from 'servequery-ui-lib/api'
import { Box, CssBaseline, ThemeProvider } from 'servequery-ui-lib/shared-dependencies/mui-material'
import { theme } from 'servequery-ui-lib/theme/index'

import type { DashboardInfoModel } from 'servequery-ui-lib/api/types'
import { ThemeToggle } from 'servequery-ui-lib/components/ThemeToggle'
import { StandaloneSnapshotWidgets } from 'servequery-ui-lib/standalone/app'

export function drawDashboard(
  dashboard: DashboardInfoModel,
  additionalGraphs: Map<string, AdditionalGraphInfo>,
  tagId: string
) {
  const element = document.getElementById(tagId)
  if (element) {
    ReactDOM.createRoot(element).render(
      <React.StrictMode>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Box display={'flex'} justifyContent={'flex-end'} p={1}>
            <ThemeToggle />
          </Box>
          <StandaloneSnapshotWidgets dashboard={dashboard} additionalGraphs={additionalGraphs} />
        </ThemeProvider>
      </React.StrictMode>
    )
  }
}

// @ts-ignore
window.drawDashboard = drawDashboard
