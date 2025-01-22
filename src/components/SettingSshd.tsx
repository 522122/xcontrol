import { call } from "@decky/api";
import { PanelSectionRow, ToggleField } from "@decky/ui";
import { useState } from "react";
import { useData } from "../DataContext";
import { IoCodeWorkingSharp } from "react-icons/io5";

function osValueToState(osValue: string) {
  return osValue === "start";
}

function stateToOsValue(state: boolean) {
  return state ? "start" : "stop";
}

export default function () {
  const osValue = useData<string>((state) => state.sshd);
  const [value, setValue] = useState<boolean>(osValueToState(osValue));

  const isOutOfSync = value !== osValueToState(osValue);

  const handleChange = (value: boolean) => {
    setValue(value);
    call("write", [stateToOsValue(value), "sshd"]);
  };

  return (
    <PanelSectionRow>
      <ToggleField
        label="SSHD"
        checked={value}
        onChange={handleChange}
        description={isOutOfSync && <IoCodeWorkingSharp />}
      />
    </PanelSectionRow>
  );
}
