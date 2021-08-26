import DeleteButton from "../Shared/DeleteButton";

export default function AwardForm({ award, handleChange, handleDelete }) {
  return (
    <div className="pt-4 pb-4 relative">
      <input
        type="text"
        className="details-form-style w-1/2"
        placeholder="수상내역"
        value={award.name}
        onChange={(e) => handleChange(award.id, "name", e.target.value)}
      />
      <input
        type="text"
        className="details-form-style w-3/4"
        placeholder="상세내역을 기록해주세요."
        value={award.description}
        onChange={(e) => handleChange(award.id, "description", e.target.value)}
      />
      <DeleteButton handleDelete={handleDelete} />
    </div>
  );
}
