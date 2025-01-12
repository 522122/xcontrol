import { call } from "@decky/api";
import { createContext, useContext, useEffect, useRef, useState } from "react";

const dataContext = createContext<Record<string, any> | null>(null);

export const useData = <T,>(selector: (state: Record<string, any>) => T) => {
  const state = useContext(dataContext);
  if (state == null)
    throw new Error("useData must be used within a DataProvider");
  return selector(state);
};

const getOsState = async (onComplete: (arg0: any) => void) => {
  const result = await call<[], Record<string, string>>("read");
  onComplete(result);
};

export const DataProvider: React.FC<{
  children: React.ReactNode;
}> = ({ children }) => {
  const [state, setState] = useState<Record<string, any> | null>(null);

  const timer = useRef<{
    t: NodeJS.Timeout | null;
    isMounted: boolean;
  }>({
    t: null,
    isMounted: true,
  });

  const startPolling = () => {
    getOsState((result) => {
      if (timer.current.isMounted) {
        setState(result);
        timer.current.t = setTimeout(startPolling, 2000);
      }
    });
  };

  useEffect(() => {
    startPolling();
    return () => {
      if (timer.current.t != null) {
        clearTimeout(timer.current.t);
      }
      timer.current.isMounted = false;
    };
  }, []);

  if (state == null) {
    return <div>Loading...</div>;
  }

  return <dataContext.Provider value={state}>{children}</dataContext.Provider>;
};
