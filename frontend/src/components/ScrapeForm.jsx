import React, { useState } from "react";
import { Form, Input, Select, Slider } from "antd";
import IFrameWebsitePreview from "./IFramePreview";
import { useAuth } from "../contexts/AuthContext";
import JobHandler from "./JobHandler";
import "../css/ScrapeForm.css";
import bdLogo from "../assets/bd-logo.png";

const { Option } = Select;
const { TextArea } = Input;

const ScrapeForm = ({ showLogin }) => {
  const { isLoggedIn } = useAuth();
  const [scrapeData, setScrapeData] = useState({
    url: "",
    language: "python",
    library: "selenium",
    prompt: "",
    performance: 1,
  });

  const handleInputChange = (name, value) => {
    setScrapeData({ ...scrapeData, [name]: value });
  };

  return (
    <Form className="scrape-form" layout="vertical">
      <div className="row">
        <Form.Item label="Target Website" className="item">
          <Input
            value={scrapeData.url}
            onChange={(e) => handleInputChange("url", e.target.value)}
            placeholder="https://example.com"
          />
        </Form.Item>
        {/*showPreview && <IFrameWebsitePreview url={scrapeData.url} />*/}
        <Form.Item label="Language" className="item">
          <Select
            value={scrapeData.language}
            onChange={(value) => handleInputChange("language", value)}
          >
            <Option value="python">Python</Option>
            <Option value="javascript">JavaScript</Option>
          </Select>
        </Form.Item>
        <Form.Item label="Library" className="item">
          <Select
            value={scrapeData.library}
            onChange={(value) => handleInputChange("library", value)}
          >
            <Option value="selenium">Selenium</Option>
            <Option value="playwright">Playwright</Option>
            <Option value="puppeteer">Puppeteer</Option>
          </Select>
        </Form.Item>
      </div>
      <Form.Item label="Prompt">
        <TextArea
          value={scrapeData.prompt}
          onChange={(e) => handleInputChange("prompt", e.target.value)}
          rows={4}
          placeholder="Use simple words. For example: products and price "
        />
      </Form.Item>
      <Form.Item label="Performance">
        <Slider
          min={1}
          max={4}
          value={scrapeData.performance}
          onChange={(value) => handleInputChange("performance", value)}
        />
      </Form.Item>
      <JobHandler scrapeData={scrapeData} login={showLogin} />
      <div style={{marginTop: 20}}>
        <span className="powered-by">
          <p>POWERED BY</p>
          <img src={bdLogo} />
        </span>
        {!isLoggedIn && (
          <p className="login-msg">Please log in to generate scraping code.</p>
        )}
      </div>
    </Form>
  );
};

export default ScrapeForm;
