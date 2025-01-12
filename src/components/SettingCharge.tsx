import { call } from "@decky/api";
import { PanelSectionRow, SliderField } from "@decky/ui";
import { useState } from "react";
import { useData } from "../DataContext";
import { IoCodeWorkingSharp } from "react-icons/io5";

export default function () {
  const osValue = useData<string>((state) => state.charge);
  const [value, setValue] = useState<number>(Number(osValue));

  const isOutOfSync = value !== Number(osValue);

  const handleChange = (value: number) => {
    setValue(value);
    call("write", ["charge", value]);
  };

  return (
    <PanelSectionRow>
      <SliderField
        label="Battery charge limit"
        value={value}
        onChange={handleChange}
        description={isOutOfSync && <IoCodeWorkingSharp />}
        showValue
        validValues="steps"
        min={50}
        max={100}
        step={10}
      />
    </PanelSectionRow>
  );
}
