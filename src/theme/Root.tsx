import React from "react";
import useDragonflyLatestVersion from "../hooks/useDragonflyLatestVersion";

const Root = ({ children }) => {
  useDragonflyLatestVersion();

  return <>{children}</>;
};

export default Root;
