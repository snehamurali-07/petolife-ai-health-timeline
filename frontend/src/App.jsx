import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeDocument = async () => {
    if (!file) {
      setError("Please select a health document.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(
        `${API_URL}/analyze`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResult(response.data.data);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to analyze document. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const getEventIcon = (type) => {
    const icons = {
      checkup: "🩺",
      vaccination: "💉",
      medication: "💊",
      laboratory: "🧪",
      lab: "🧪",
    };

    return icons[type?.toLowerCase()] || "🐾";
  };

  return (
    <div className="app">

      {/* NAVBAR */}
      <header className="navbar">
        <div className="brand">
          <div className="brand-mark">P</div>

          <div>
            <div className="brand-name">PetOlife</div>
            <div className="brand-tagline">Better care. Happier lives.</div>
          </div>
        </div>

        <div className="nav-label">
          AI Health Timeline
        </div>
      </header>


      <main className="container">

        {/* HERO */}
        <section className="hero">

          <div className="hero-text">

            <span className="eyebrow">
              PET HEALTH INTELLIGENCE
            </span>

            <h1>
              Your pet's health,
              <br />
              <span>all in one timeline.</span>
            </h1>

            <p>
              Upload veterinary records and let AI turn
              scattered medical information into a simple,
              organized health timeline.
            </p>

          </div>

          <div className="hero-paw">
            🐾
          </div>

        </section>


        {/* UPLOAD */}
        <section className="upload-card">

          <div className="section-heading">

            <div className="heading-icon">
              ↑
            </div>

            <div>
              <h2>Upload a health record</h2>

              <p>
                PDF, JPG or PNG veterinary documents
              </p>
            </div>

          </div>


          <label className="drop-zone">

            <input
              type="file"
              accept=".pdf,.png,.jpg,.jpeg"
              onChange={(e) => {
                setFile(e.target.files[0]);
                setError("");
              }}
            />

            <div className="upload-icon">
              ↑
            </div>

            <strong>
              {file
                ? file.name
                : "Choose a health document"}
            </strong>

            <span>
              {file
                ? "Ready to analyze"
                : "Click to browse your files"}
            </span>

          </label>


          <button
            className="primary-button"
            onClick={analyzeDocument}
            disabled={loading}
          >

            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing record...
              </>
            ) : (
              <>
                Analyze Health Record
                <span>→</span>
              </>
            )}

          </button>


          {error && (
            <div className="error">
              <span>!</span>
              {error}
            </div>
          )}

        </section>


        {/* RESULTS */}
        {result && (
          <section className="results">

            {/* PET PROFILE */}
            <div className="pet-profile">

              <div className="pet-avatar">
                🐶
              </div>

              <div className="pet-details">

                <span className="eyebrow">
                  HEALTH PROFILE
                </span>

                <h2>
                  {result.pet_name || "Your Pet"}
                </h2>

                <p>
                  {result.document_type ||
                    "Veterinary Health Record"}
                </p>

              </div>

              <div className="status-badge">
                <span></span>
                Record analyzed
              </div>

            </div>


            {/* SUMMARY */}
            {result.summary && (
              <div className="summary-card">

                <div className="card-label">
                  AI SUMMARY
                </div>

                <p>
                  {result.summary}
                </p>

              </div>
            )}


            {/* TIMELINE */}
            {result.events?.length > 0 && (
              <section className="timeline-section">

                <div className="section-title">

                  <div>
                    <span className="eyebrow">
                      HEALTH HISTORY
                    </span>

                    <h2>
                      Health Timeline
                    </h2>
                  </div>

                  <span className="event-count">
                    {result.events.length} events
                  </span>

                </div>


                <div className="timeline">

                  {result.events.map((event, index) => (

                    <div
                      className="timeline-item"
                      key={index}
                    >

                      <div className="timeline-line">

                        <div className="timeline-dot">
                          {getEventIcon(event.type)}
                        </div>

                      </div>


                      <div className="timeline-card">

                        <div className="timeline-top">

                          <span className="event-type">
                            {event.type}
                          </span>

                          <span className="event-date">
                            {event.date}
                          </span>

                        </div>

                        <h3>
                          {event.title}
                        </h3>

                        <p>
                          {event.description}
                        </p>

                        <span className="event-status">
                          ✓ {event.status}
                        </span>

                      </div>

                    </div>

                  ))}

                </div>

              </section>
            )}


            {/* DATA GRID */}
            <div className="data-grid">

              {/* MEDICATIONS */}
              {result.medications?.length > 0 && (
                <div className="info-card">

                  <div className="info-card-header">
                    <div className="info-icon medicine">
                      💊
                    </div>

                    <div>
                      <span>MEDICATION</span>
                      <h3>Current Medicines</h3>
                    </div>
                  </div>

                  {result.medications.map(
                    (medication, index) => (

                      <div
                        className="medicine-item"
                        key={index}
                      >

                        <strong>
                          {medication.name}
                        </strong>

                        <p>
                          {medication.strength}
                        </p>

                        <div className="medicine-meta">
                          <span>
                            {medication.frequency}
                          </span>

                          <span>
                            {medication.duration}
                          </span>
                        </div>

                      </div>

                    )
                  )}

                </div>
              )}


              {/* VACCINATIONS */}
              {result.vaccinations?.length > 0 && (
                <div className="info-card">

                  <div className="info-card-header">
                    <div className="info-icon vaccine">
                      💉
                    </div>

                    <div>
                      <span>PREVENTIVE CARE</span>
                      <h3>Vaccinations</h3>
                    </div>
                  </div>

                  {result.vaccinations.map(
                    (vaccine, index) => (

                      <div
                        className="vaccine-item"
                        key={index}
                      >

                        <strong>
                          {vaccine.name}
                        </strong>

                        <p>
                          Next due
                        </p>

                        <b>
                          {vaccine.next_due ||
                            "Not specified"}
                        </b>

                      </div>

                    )
                  )}

                </div>
              )}

            </div>


            {/* LAB RESULTS */}
            {result.lab_results?.length > 0 && (
              <div className="info-card full-width">

                <div className="info-card-header">

                  <div className="info-icon lab">
                    🧪
                  </div>

                  <div>
                    <span>DIAGNOSTICS</span>
                    <h3>Laboratory Results</h3>
                  </div>

                </div>


                <div className="lab-grid">

                  {result.lab_results.map(
                    (lab, index) => (

                      <div
                        className="lab-item"
                        key={index}
                      >

                        <span>
                          {lab.name}
                        </span>

                        <strong>
                          {lab.value}
                          {" "}
                          {lab.unit}
                        </strong>

                      </div>

                    )
                  )}

                </div>

              </div>
            )}


            {/* AI INSIGHTS */}
            {result.insights?.length > 0 && (
              <div className="insights-card">

                <div className="insight-heading">

                  <div className="ai-icon">
                    ✦
                  </div>

                  <div>
                    <span>AI POWERED</span>
                    <h2>Health Insights</h2>
                  </div>

                </div>


                <div className="insights-list">

                  {result.insights.map(
                    (insight, index) => (

                      <div
                        className="insight"
                        key={index}
                      >

                        <span>✓</span>

                        <p>
                          {insight}
                        </p>

                      </div>

                    )
                  )}

                </div>

              </div>
            )}

          </section>
        )}

      </main>


      {/* FOOTER */}
      <footer>
        <strong>PetOlife</strong>
        <span>AI-assisted pet health management</span>
      </footer>

    </div>
  );
}

export default App;