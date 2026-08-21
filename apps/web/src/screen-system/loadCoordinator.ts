import type { DataSourceId, ScreenContext } from "./contracts";
import { dataSources, type ScreenModel } from "./dataSources";

export class ScreenLoadCoordinator {
  private controller: AbortController | null = null;

  load(source: DataSourceId, context: ScreenContext): Promise<ScreenModel> {
    this.controller?.abort();
    this.controller = new AbortController();
    return dataSources[source](context, this.controller.signal);
  }

  abort(): void {
    this.controller?.abort();
    this.controller = null;
  }
}
