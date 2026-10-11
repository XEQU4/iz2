export interface CosmicScene {
  setActive(active: boolean): void;
  destroy(): void;
}
export function mountCosmicScene(
  host: HTMLElement,
  options?: { stars?: boolean },
): CosmicScene;
