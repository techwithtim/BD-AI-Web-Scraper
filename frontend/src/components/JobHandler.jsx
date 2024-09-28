import React, { useState, useEffect } from "react";
import { message } from "antd";
import { startAiScrape, getAiScrapeStatus } from "../services/api";
import { ScraperStatus } from "../enums/status";
import JobResult from "./JobResult";
import JobStatusDisplay from "./JobStatusDisplay";
import { useAuth } from "../contexts/AuthContext";
import "../css/JobHandler.css";

const JobHandler = ({ scrapeData, login, stopLoading }) => {
  const [jobId, setJobId] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);
  const [jobResult, setJobResult] = useState(null);
  const [startTime, setStartTime] = useState(null);
  const { credits, isLoggedIn } = useAuth();

  useEffect(() => {
    let intervalId;
    if (
      jobId &&
      jobStatus !== ScraperStatus.COMPLETED &&
      jobStatus !== ScraperStatus.FAILED
    ) {
      intervalId = setInterval(checkJobStatus, 5000); // Check every 5 seconds
    }
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [jobId, jobStatus]);

  useEffect(() => {
    if (scrapeData.bdMode !== null && scrapeData.bdMode !== undefined) {
      handleStartJob(scrapeData.bdMode)
    } 

  }, [scrapeData.bdMode])

  const checkJobStatus = async () => {
    try {
      const response = await getAiScrapeStatus(jobId);
      setJobStatus(response.status);
      if (
        response.status === ScraperStatus.COMPLETED ||
        response.status === ScraperStatus.FAILED
      ) {
        setJobResult(response.result);
        stopLoading(false);
      }
    } catch (error) {
      console.error("Error checking job status:", error);
      message.error("Failed to check job status");
      setJobStatus(ScraperStatus.FAILED);
    }
  };

  const handleStartJob = async (withBd = false) => {
    if (!isLoggedIn) {
      return login();
    }

    if (credits === 0) {
      return message.error("Insufficient credits.");
    }

    try {
      const response = await startAiScrape(scrapeData);
      setJobId(response.job_id);
      setJobStatus(ScraperStatus.STARTED);
      setStartTime(new Date());
      message.success("Scrape job started successfully");
    } catch (error) {
      console.error("Error starting scrape job:", error);
      message.error("Failed to start scrape job");
    } 
  };

  return (
    <div>
      {jobStatus && (
        <div style={{ marginTop: "20px" }}>
          <JobStatusDisplay status={jobStatus} startTime={startTime} />
        </div>
      )}
      {jobResult && (
        <JobResult result={jobResult} language={scrapeData.language} />
      )}
    </div>
  );
};

export default JobHandler;
