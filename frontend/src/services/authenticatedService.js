import httpCommon from "./httpCommon";

export const isAuthenticated = async () => {
  const token = localStorage.getItem("access_token");
  if (!token) return false;

  try {
    await httpCommon.get("/users/protected-route/", {
      headers: { Authorization: `Bearer ${token}` },
    });

    return true;
  } catch (error) {
    return false;
  }
};
