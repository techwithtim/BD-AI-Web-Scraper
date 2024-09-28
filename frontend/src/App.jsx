import React, { useState, useEffect } from "react";
import { Button, message } from "antd";
import ScrapeForm from "./components/ScrapeForm";
import LoginModal from "./components/LoginModal";
import RegisterModal from "./components/RegisterModal";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { getUserCredits } from "./services/api";
import UserJobs from "./components/UserJobs";
import Navbar from "./components/NavBar";
import Footer from "./components/Footer"
import "@fontsource/inter";
import "./App.css";


const AppContent = () => {
  const { isLoggedIn, logout, credits, setCredits } = useAuth();
  const [loginModalVisible, setLoginModalVisible] = useState(false);
  const [registerModalVisible, setRegisterModalVisible] = useState(false);

  useEffect(() => {
    if (isLoggedIn) {
      fetchUserCredits();
    }
  }, [isLoggedIn]);

  const fetchUserCredits = async () => {
    try {
      const userCredits = await getUserCredits();
      setCredits(userCredits);
    } catch (error) {
      message.error("Error fetching user credits");
    }
  };

  const handleLogout = () => {
    logout();
    setCredits(0);
  };

  const switchToRegister = () => {
    setLoginModalVisible(false);
    setRegisterModalVisible(true);
  };

  const switchToLogin = () => {
    setRegisterModalVisible(false);
    setLoginModalVisible(true);
  };

  return (
    <div className="main">
      <Navbar
        credits={credits}
        isLoggedIn={isLoggedIn}
        login={() => setLoginModalVisible(true)}
        logout={handleLogout}
      />
      <div className="content">
        <div className="header">
          <h1>AI Web Scraper</h1>
          <h1>Script Generator</h1>
          <p>Power your AI apps with clean data crawled from any website.</p>
          <p>
            It's also <a href="">open-source</a>
          </p>
        </div>
        <ScrapeForm showLogin={() => setLoginModalVisible(true)} />
        {isLoggedIn && (
          <div style={{ marginTop: 20 }}>
            <UserJobs />
          </div>
        )}
        <LoginModal
          visible={loginModalVisible}
          onCancel={() => setLoginModalVisible(false)}
          onSwitchToRegister={switchToRegister}
        />
        <RegisterModal
          visible={registerModalVisible}
          onCancel={() => setRegisterModalVisible(false)}
          onSwitchToLogin={switchToLogin}
        />
      </div>
      <Footer />
    </div>
  );
};

const App = () => (
  <AuthProvider>
    <AppContent />
  </AuthProvider>
);

export default App;
