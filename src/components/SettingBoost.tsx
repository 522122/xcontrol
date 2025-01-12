import { useState } from "react";
import { useData } from "../DataContext";
import { PanelSectionRow, ToggleField } from "@decky/ui";
import { call } from "@decky/api";
import { IoCodeWorkingSharp } from "react-icons/io5";

export default function () {
  const osValue = useData<string>((state) => state.boost);
  const [value, setValue] = useState<boolean>(osValue === "1");

  const isOutOfSync = Number(value) !== Number(osValue);

  const handleChange = (value: boolean) => {
    setValue(value);
    call("write", ["boost", Number(value)]);
  };

  return (
    <PanelSectionRow>
      <ToggleField
        label="Cpu Boost"
        checked={value}
        onChange={handleChange}
        description={isOutOfSync && <IoCodeWorkingSharp />}
      />
    </PanelSectionRow>
  );
}
