import type { BatchMetricDataModel, DashboardPanelPlotModel } from 'servequery-ui-lib/api/types/v2'
import type { PanelComponentType } from 'servequery-ui-lib/components/v2/Dashboard/HelperComponents/DrawDashboardPanels'
import { RenderPanelByDataFetchGeneralComponent } from 'servequery-ui-lib/components/v2/Dashboard/HelperComponents/RenderPanelByDataFetchGeneralComponent'
import invariant from 'tiny-invariant'
import { useProjectInfo } from '~/contexts/project'
import { useLoader } from '~/routes/hooks'

const RenderPanelByDataFetch = ({ panel }: { panel: DashboardPanelPlotModel }) => {
  const { project } = useProjectInfo()
  invariant(project)

  const { id: projectId } = project

  const panelPointsFetcher = useLoader('/projects/:projectId/load-panel-points')

  const loadDataForPanel = () =>
    panelPointsFetcher.load({
      query: {
        body: JSON.stringify({
          series_filter: panel.values.map((s) => ({
            metric: s.metric,
            tags: s.tags ?? [],
            metadata: s.metadata ?? {},
            metric_labels: s.metric_labels ?? {}
          }))
        } satisfies BatchMetricDataModel)
      },
      paramsToReplace: { projectId }
    })

  const data = panelPointsFetcher.data

  return (
    <RenderPanelByDataFetchGeneralComponent
      panel={panel}
      loadDataForPanel={loadDataForPanel}
      data={data}
    />
  )
}

export const PanelComponent: PanelComponentType = RenderPanelByDataFetch
