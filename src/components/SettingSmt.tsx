import { useState } from "react";
import { useData } from "../DataContext";
import { PanelSectionRow, ToggleField } from "@decky/ui";
import { call } from "@decky/api";
import { IoCodeWorkingSharp } from "react-icons/io5";

export default function () {
  const osValue = useData<string>((state) => state.smt);
  const [value, setValue] = useState<boolean>(osValue === "1");

  const isOutOfSync = Number(value) !== Number(osValue);

  const handleChange = (value: boolean) => {
    setValue(value);
    call("write", ["smt", Number(value)]);
  };

  return (
    <PanelSectionRow>
      <ToggleField
        label="SMT"
        checked={value}
        onChange={handleChange}
        description={isOutOfSync && <IoCodeWorkingSharp />}
      />
    </PanelSectionRow>
  );
}
