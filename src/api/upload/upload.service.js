import api from "../axios";

export const uploadCsv = async (file) => {

  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/upload/upload-csv",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    }
  );

  return response.data;
};