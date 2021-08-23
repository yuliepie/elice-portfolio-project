export default function CertForm({ cert, handleChange }) {
  return (
    <div className="py-4">
      <input
        type="text"
        className="details-form-style w-1/2"
        placeholder="자격증"
        value={cert.name}
        onChange={(e) => handleChange(cert.id, "name", e.target.value)}
      />
      <input
        type="text"
        className="details-form-style w-2/3"
        placeholder="발급기관"
        value={cert.provider}
        onChange={(e) => handleChange(cert.id, "provider", e.target.value)}
      />
      <div className="mt-2">
        <label>
          <span className="text-gray-700 text-sm">취득 날짜: </span>
          <input
            className="text-sm"
            onChange={(e) =>
              handleChange(cert.id, "acquired_date", e.target.value)
            }
            value={cert.acquired_date}
            type="date"
          />
        </label>
      </div>
    </div>
  );
}
