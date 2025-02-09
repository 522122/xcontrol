import { call } from "@decky/api";
import { PanelSectionRow, SliderField } from "@decky/ui";
import { useState } from "react";
import { useData } from "../DataContext";
import { IoCodeWorkingSharp } from "react-icons/io5";

export default function () {
  const osValue = useData<string>((state) => state.cores);
  const [value, setValue] = useState<number>(Number(osValue));

  const isOutOfSync = value !== Number(osValue);

  const handleChange = (value: number) => {
    setValue(value);
    call("write", ["cores", value]);
  };

  return (
    <PanelSectionRow>
      <SliderField
        label="Cores"
        value={value}
        onChange={handleChange}
        description={isOutOfSync && <IoCodeWorkingSharp />}
        showValue
        min={2}
        max={8}
        step={1}
      />
    </PanelSectionRow>
  );
}
