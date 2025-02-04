import httpCommon from "./httpCommon";

const signinUser = async (email, password) => {
  try {
    const response = await httpCommon.post("/users/signin/", {
      email,
      password,
    });
    return response.data;
  } catch (error) {
    console.error("Sign-in error:", error);
    throw error;
  }
};

const signupUser = async (name, email, password) => {
  try {
    const response = await httpCommon.post("/users/signup/", {
      name,
      email,
      password,
    });
    return response.data;
  } catch (error) {
    console.error("Sign-up error:", error);
    throw error;
  }
};

export { signinUser, signupUser };
