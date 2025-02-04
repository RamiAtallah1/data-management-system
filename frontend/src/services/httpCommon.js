import axios from "axios";

const httpCommon = axios.create({
  baseURL: "http://localhost:8000/api/",
});

export default httpCommon;
