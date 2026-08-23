import api from "./client";

export const getPet = async (petId) => {
  const response = await api.get(`/pets/${petId}`);
  return response.data;
};

export const createPet = async (petData) => {
  const response = await api.post("/pets/", petData);
  return response.data;
};