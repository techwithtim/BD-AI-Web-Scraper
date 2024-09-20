import React, { useState, useEffect } from 'react';
import { Button, message } from 'antd';
import ScrapeForm from './components/ScrapeForm';
import LoginModal from './components/LoginModal';
import RegisterModal from './components/RegisterModal';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { getUserCredits } from './services/api';
import UserJobs from './components/UserJobs';

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
      message.error('Error fetching user credits');
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
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>AI Scraper</h1>
      {isLoggedIn && (
        <div>
          <p>Credits: {credits}</p>
          <Button onClick={handleLogout}>Logout</Button>
        </div>
      )}
      <ScrapeForm showLogin={() => setLoginModalVisible(true)} />
      <div style={{ marginTop: 20 }}>
        <UserJobs />
      </div>
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
  );
};

const App = () => (
  <AuthProvider>
    <AppContent />
  </AuthProvider>
);

export default App;