import { useEffect, useState } from "react";
import api from "../api";

function PetDashboard() {
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchPets();
  }, []);

  const fetchPets = async () => {
    try {
      const response = await api.get("/pets/");
      setPets(response.data);
    } catch (err) {
      console.error(err);
      setError("Unable to load pets.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <p>Loading pets...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <h1>Your Pets</h1>

      {pets.length === 0 ? (
        <p>No pets found.</p>
      ) : (
        <div>
          {pets.map((pet) => (
            <div key={pet.id}>
                <h2>🐕 {pet.name}</h2>

                <p>
                {pet.species}
                {pet.breed ? ` • ${pet.breed}` : ""}
                </p>

                {pet.current_weight && (
                <p>Weight: {pet.current_weight} kg</p>
                )}

                <button>
                View Health Timeline →
                </button>
            </div>
            ))}
        </div>
      )}
    </div>
  );
}

export default PetDashboard;