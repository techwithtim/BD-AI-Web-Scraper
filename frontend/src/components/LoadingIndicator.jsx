import React from "react";
import { Spin } from "antd";

const LoadingIndicator = () => {
  return (
    <div style={{ display: "flex", alignItems: "center", fontSize: "16px", color: "#9ca3af", justifyContent: "center", fontWeight: 400 }}>
      <Spin size="small" style={{ marginRight: "10px", }} />
      <em>Generating code...</em>
    </div>
  );
};

export default LoadingIndicator;
