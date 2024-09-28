import React, { useState } from "react";
import { Form, Input, Select, Slider, Button, message } from "antd";
import { useAuth } from "../contexts/AuthContext";
import JobHandler from "./JobHandler";
import LoadingIndicator from "./LoadingIndicator";
import "../css/ScrapeForm.css";
import bdLogo from "../assets/bd-logo.png";
import { ScraperStatus } from "../enums/status";

const { Option } = Select;
const { TextArea } = Input;

const ScrapeForm = ({ showLogin, fetchCredits, fetchJobs }) => {
  const { isLoggedIn } = useAuth();
  const [form] = Form.useForm(); // Form instance for handling form state
  const [scrapeData, setScrapeData] = useState({
    url: "",
    language: "python",
    library: "selenium",
    prompt: "",
    performance: 1,
  });
  const [buttonType, setButtonType] = useState(null);
  const [loading, setLoading] = useState(false);
  const promptMaxLength = 100;

  const handleInputChange = (name, value) => {
    setScrapeData({ ...scrapeData, [name]: value });
  };

  const handleSubmit = (values) => {
    if (loading) return;
    setLoading(true);
    setScrapeData({
      ...values,
      bdMode: buttonType === "normal" ? false : true,
    });
  };

  const stopLoading = (status) => {
    if (!loading) return;
    if (status === ScraperStatus.COMPLETED) message.success("Job completed.");
    setScrapeData({ ...scrapeData, bdMode: null });
    setLoading(false);
    fetchCredits();
    fetchJobs();
  };

  return (
    <Form
      form={form}
      className="scrape-form"
      layout="vertical"
      onFinish={handleSubmit}
      initialValues={scrapeData} // Set initial form values
    >
      <div className="row">
        <Form.Item
          label="Target Website"
          name="url"
          className="item"
          required={false}
          rules={[
            { required: true, message: "Please enter the target website URL" },
            { type: "url", message: "Please enter a valid URL" },
          ]}
        >
          <Input
            value={scrapeData.url}
            onChange={(e) => handleInputChange("url", e.target.value)}
            placeholder="https://example.com"
          />
        </Form.Item>

        <Form.Item
          label="Language"
          name="language"
          className="item"
          required={false}
          rules={[
            { required: true, message: "Please select a programming language" },
          ]}
        >
          <Select
            value={scrapeData.language}
            onChange={(value) => handleInputChange("language", value)}
          >
            <Option value="python">Python</Option>
            <Option value="javascript">JavaScript</Option>
          </Select>
        </Form.Item>

        <Form.Item
          label="Library"
          name="library"
          required={false}
          className="item"
          rules={[{ required: true, message: "Please select a library" }]}
        >
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

      <Form.Item
        label="Prompt"
        name="prompt"
        rules={[
          { required: true, message: "Please enter a prompt" },
          {
            max: promptMaxLength,
            message: `Prompt cannot exceed ${promptMaxLength} characters`,
          },
          { min: 5, message: `Prompt must be at least 5 characters` },
        ]}
        required={false}
      >
        <TextArea
          value={scrapeData.prompt}
          onChange={(e) => handleInputChange("prompt", e.target.value)}
          rows={4}
          maxLength={promptMaxLength}
          placeholder="Use simple words. For example: products and price"
        />
      </Form.Item>

      <Form.Item label="Performance" name="performance">
        <Slider
          min={1}
          max={4}
          value={scrapeData.performance}
          onChange={(value) => handleInputChange("performance", value)}
        />
      </Form.Item>

      {!loading ? (
        <div className="buttons">
          <Button
            className="code-btn"
            htmlType="submit"
            onClick={() => setButtonType("normal")}
          >
            Generate Code
          </Button>
          <Button
            className="bd-btn"
            htmlType="submit"
            onClick={() => setButtonType("bd")}
          >
            Generate with BrightData
          </Button>
        </div>
      ) : (
        <LoadingIndicator />
      )}

      <div style={{ marginTop: 20 }}>
        <span className="powered-by">
          <p>POWERED BY</p>
          <img src={bdLogo} alt="bd logo" />
        </span>
        {!isLoggedIn && (
          <p className="login-msg">
            Please <a onClick={showLogin}>login</a> to generate scraping code.
          </p>
        )}
      </div>
      {isLoggedIn && (
        <JobHandler
          scrapeData={scrapeData}
          login={showLogin}
          stopLoading={stopLoading}
        />
      )}
    </Form>
  );
};

export default ScrapeForm;
