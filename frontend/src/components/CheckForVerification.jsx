import React, { useEffect, useState } from "react";
import { verify } from "../services/api";
import { Modal } from "antd";
import "../css/CheckVerification.css";
import { useAuth } from "../contexts/AuthContext";

function Verification() {
  const [open, setOpen] = useState(false);
  const [verificationStatus, setVerificationStatus] = useState(null);
  const {setIsLoggedIn} = useAuth()

  useEffect(() => {
    const checkForVerificationToken = async () => {
      if (verificationStatus) return
      const searchParams = new URLSearchParams(window.location.search);
      const token = searchParams.get("token");

      if (token) {
        try {
          const result = await verify(token);
          setVerificationStatus(result);

          if (result.success) {
            setTimeout(() => {
              setIsLoggedIn()
              window.location.href = '/'; 
            }, 3000);
          }
        } catch (error) {
          console.error("Verification error:", error);
          setVerificationStatus({
            success: false,
            message: "Verification failed. Please try again.",
          });
        }
        setOpen(true);
      }
    };

    checkForVerificationToken();

    // Set up an event listener for URL changes
    const handleUrlChange = () => {
      setOpen(false);
      checkForVerificationToken();
    };

    window.addEventListener("popstate", handleUrlChange);

    // Clean up the event listener when the component unmounts
    return () => {
      window.removeEventListener("popstate", handleUrlChange);
    };
  }, []);

  return (
    <Modal
      open={open}
      onCancel={() => setOpen(false)}
      footer={null}
      className="modal"
    >
      <h3>Email Verification</h3>
      {verificationStatus && (
        <div
          className={`verification-message ${
            verificationStatus.success ? "success" : "error"
          }`}
        >
          {verificationStatus.message}
          {verificationStatus.success && <p>You will be redirected to the dashboard shortly...</p>}
        </div>
      )}
    </Modal>
  );
}

export default Verification;
