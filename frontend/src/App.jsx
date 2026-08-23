import { useEffect, useState } from "react";
import { getPet } from "./api/pets";

function App() {
  const [pet, setPet] = useState(null);
  const [error, setError] = useState(null);

  const petId = "a995640d-03d5-4210-9227-e78a2c8dd391";

  useEffect(() => {
    const loadPet = async () => {
      try {
        const data = await getPet(petId);

        setPet(data);
      } catch (error) {
        console.error(error);
        setError("Could not load pet");
      }
    };

    loadPet();
  }, []);

  return (
    <div>
      <h1>PetOlife AI Health Timeline</h1>

      {error && <p>{error}</p>}

      {!pet && !error && <p>Loading pet...</p>}

      {pet && (
        <div>
          <h2>{pet.name}</h2>

          <p>Species: {pet.species}</p>

          <p>Breed: {pet.breed}</p>

          <p>Weight: {pet.current_weight} kg</p>
        </div>
      )}
    </div>
  );
}

export default App;