import httpCommon from "./httpCommon";

const getAllSchemas = async () => {
  const token = localStorage.getItem("access_token");

  const response = await httpCommon.get("/schemas/", {
    headers: { Authorization: `Bearer ${token}` },
  });

  return response.data;
};

const getSchemasWithSearchAndSort = async (searchQuery, sortField) => {
  const token = localStorage.getItem("access_token");

  try {
    const response = await httpCommon.get("/schemas/", {
      params: {
        search: searchQuery,
        ordering: sortField,
      },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching schemas:", error);
    throw error;
  }
};

const postSchema = async (tableName, fields) => {
  const token = localStorage.getItem("access_token");

  const response = await httpCommon.post(
    "/schemas/create/",
    {
      table_name: tableName,
      fields: fields,
    },
    {
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    }
  );

  return response.data;
};

const postData = async (tableName, formData) => {
  const token = localStorage.getItem("access_token");

  try {
    const response = await httpCommon.post(`schemas/import/${tableName}/`, formData, {
      headers: { "Content-Type": "multipart/form-data", Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    console.error("Error importing data:", error);
    throw error;
  }
};

const addFields = async (tableName, fields) => {
  const token = localStorage.getItem("access_token");

  const response = await httpCommon.patch(
    `/schemas/add-fields/${tableName}/`,
    {
      fields: fields,
    },
    {
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    }
  );

  return response.data;
};

const deleteSchema = async (tableName) => {
  const token = localStorage.getItem("access_token");

  const response = await httpCommon.delete(`/schemas/delete/${tableName}/`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  return response.data;
};

export {
  getAllSchemas,
  getSchemasWithSearchAndSort,
  postSchema,
  postData,
  addFields,
  deleteSchema,
};
