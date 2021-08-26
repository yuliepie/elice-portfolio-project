import DeleteButton from "../Shared/DeleteButton";

export default function CertForm({ cert, handleChange, handleDelete }) {
  return (
    <div className="py-4 relative">
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
        <label className="inline-flex items-center gap-2">
          <input
            className="details-form-style w-auto"
            onChange={(e) =>
              handleChange(cert.id, "acquired_date", e.target.value)
            }
            value={cert.acquired_date}
            type="date"
          />
          <span className="text-gray-700 font-bold">에 취득.</span>
        </label>
      </div>
      <DeleteButton handleDelete={handleDelete} />
    </div>
  );
}
