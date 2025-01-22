import { PanelSection, staticClasses } from "@decky/ui";
import { definePlugin } from "@decky/api";
import { GiPowerLightning } from "react-icons/gi";
import { DataProvider } from "./DataContext";
import SettingCores from "./components/SettingCores";
import SettingTdp from "./components/SettingTdp";
import SettingSmt from "./components/SettingSmt";
import SettingCharge from "./components/SettingCharge";
import SettingBoost from "./components/SettingBoost";
import SettingSshd from "./components/SettingSshd";

function Content() {
  // const state = useData((state) => state);

  return (
    <PanelSection>
      {/* <PanelSectionRow>
        <pre>{JSON.stringify(state, null, 2)}</pre>
      </PanelSectionRow> */}

      <SettingTdp />
      <SettingCores />
      <SettingSmt />
      <SettingBoost />
      <SettingCharge />
      <SettingSshd />

    </PanelSection>
  );
}

export default definePlugin(() => {
  return {
    // The name shown in various decky menus
    name: "X Control",
    // The element displayed at the top of your plugin's menu
    titleView: <div className={staticClasses.Title}>X Control</div>,
    // The content of your plugin's menu
    content: (
      <DataProvider>
        <Content />
      </DataProvider>
    ),
    // The icon displayed in the plugin list
    icon: <GiPowerLightning />,
    // The function triggered when your plugin unloads
    onDismount() {
      console.log("Unloading");
    },
  };
});
