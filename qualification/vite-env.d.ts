declare module "*.json?raw" {
  const source: string;
  export default source;
}

declare module "*.css" {
  const source: string;
  export default source;
}

declare const __FGA_FIXTURE_SHA256__: string;
