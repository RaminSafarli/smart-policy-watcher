import { platformUrls } from "../constants/platformsUrls";

export default function getPlatformUrl(platform: string): string {
  return platformUrls[platform];
}
