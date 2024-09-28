import React, { useState, useEffect } from "react";
import { Table, Tag, Button, message } from "antd";
import { getUserJobs, deleteJob } from "../services/api";
import JobResultViewer from "./JobResultViewer";
import { ScraperStatus } from "../enums/status";
import "../css/UserJobs.css"
import { useAuth } from "../contexts/AuthContext";

const UserJobs = () => {
    const {jobs, setJobs} = useAuth()
    const [loading, setLoading] = useState(false);
    const [selectedJob, setSelectedJob] = useState(null);
    const [resultViewerVisible, setResultViewerVisible] = useState(false);


    const handleDelete = async (jobId) => {
        if (loading) return
        setLoading(true)
        try {
            await deleteJob(jobId);
            console.log(jobId)
            message.success("Job deleted successfully");
            setJobs((jobs) => jobs.filter((job) => job._id !== jobId))
        } catch (error) {
            console.error("Failed to delete job:", error);
            message.error("Failed to delete job");
        } finally {
            setLoading(false)
        }
    };

    const handleViewResult = (job) => {
        setSelectedJob(job);
        setResultViewerVisible(true);
    };

    const columns = [
        {
            title: "Status",
            dataIndex: "status",
            key: "status",
            render: (status) => (
                <Tag
                    color={
                        status === ScraperStatus.COMPLETED
                            ? "green"
                            : status === ScraperStatus.FAILED
                                ? "red"
                                : "blue"
                    }
                >
                    {status}
                </Tag>
            ),
        },
        {
            title: "Start Time",
            dataIndex: "start_time",
            key: "start_time",
            render: (time) => new Date(time).toLocaleString(),
        },
        {
            title: "End Time",
            dataIndex: "end_time",
            key: "end_time",
            render: (time) => (time ? new Date(time).toLocaleString() : "N/A"),
        },
        {
            title: "URL",
            dataIndex: ["scrape_data", "url"],
            key: "url",
        },
        {
            title: "Action",
            key: "action",
            render: (_, record) => (
                <div className="actions">
                    <Button
                        type="primary"
                        onClick={() => handleViewResult(record)}
                        style={{ marginRight: 8 }}
                        disabled={record.status !== ScraperStatus.COMPLETED}
                        className="view-btn"
                    >
                        View Result
                    </Button>
                    <Button
                        type="danger"
                        onClick={() => handleDelete(record._id)}
                        className="delete-btn"
                    >
                        Delete
                    </Button>
                </div>
            ),
        },
    ];

    return (
        <div className="user-jobs">
            <h4>Previously Generated Scripts</h4>
            <Table
                dataSource={jobs}
                columns={columns}
                rowKey="id"
                loading={loading}
            />
            <JobResultViewer
                visible={resultViewerVisible}
                onClose={() => setResultViewerVisible(false)}
                job={selectedJob}
            />
        </div>
    );
};

export default UserJobs;
