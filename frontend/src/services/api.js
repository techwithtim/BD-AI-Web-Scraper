import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // Replace with your actual API URL

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

api.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem("refresh_token");
        const response = await axios.post(`${API_BASE_URL}/users/refresh`, {
          refresh_token: refreshToken,
        });
        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("refresh_token", response.data.refresh_token);
        api.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${response.data.access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // If refresh fails, log out the user
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export const verify = async (token) => {
  try {
    if (!token) {
      throw new Error("Verification token is missing");
    }

    // Make the API call to your backend
    const response = await api.post("/users/verify-email", { token });
    console.log(response.data)

    if (response.data.message === "Email verified successfully") {
      localStorage.setItem("access_token", response.data.access_token);
      localStorage.setItem("refresh_token", response.data.refresh_token);
      return {
        success: true,
        message: "Your email has been successfully verified!",
      };
    } else {
      return {
        success: false,
        message: response.data.message,
      };
    }
  } catch (error) {
    console.error("Email verification error:", error);

    // Handle specific error cases
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      if (error.response.status === 400) {
        return {
          success: false,
          message: "Invalid or expired verification token.",
        };
      }
    } else if (error.request) {
      // The request was made but no response was received
      return {
        success: false,
        message: "Unable to connect to the server. Please try again later.",
      };
    }

    // Generic error message for other types of errors
    return {
      success: false,
      message: "An unexpected error occurred. Please try again later.",
    };
  }
};

export const login = async (email, password) => {
  const formData = new URLSearchParams();
  formData.append("username", email); // Note: The backend expects 'username', but we're sending the email
  formData.append("password", password);

  const response = await api.post("/users/token", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
  localStorage.setItem("access_token", response.data.access_token);
  localStorage.setItem("refresh_token", response.data.refresh_token);
  return response.data;
};

export const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
};

export const register = async (email, password) => {
  const response = await api.post("/users/register", { email, password });
  return response.data;
};

export const getUserCredits = async () => {
  const response = await api.get("/users/me");
  return response.data.credits;
};

export const startAiScrape = async (data) => {
  const response = await api.post("/start-ai-scrape", data);
  return response.data;
};

export const getAiScrapeStatus = async (jobId) => {
  const response = await api.get(`/get-ai-scrape/${jobId}`);
  return response.data;
};

export const getUserJobs = async () => {
  const response = await api.get("/user-jobs");
  return response.data;
};

export const deleteJob = async (jobId) => {
  const response = await api.delete(`/delete-job/${jobId}`);
  return response.data;
};

export default api;
