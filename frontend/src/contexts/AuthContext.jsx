import React, { createContext, useState, useContext, useEffect } from 'react';
import { login as apiLogin, logout as apiLogout } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [credits, setCredits] = useState(0);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            setIsLoggedIn(true);
        }
    }, []);

    const login = async (email, password) => {
        const response = await apiLogin(email, password);
        setIsLoggedIn(true);
        return response;
    };

    const logout = () => {
        apiLogout();
        setIsLoggedIn(false);
        setCredits(0);
    };

    const value = {
        isLoggedIn,
        login,
        logout,
        credits,
        setCredits,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};