export default function AwardDetail({ award }) {
  return (
    <div className="user-detail-wrapper">
      <h3 className="user-detail-title mt-1">{award.name}</h3>
      <p className="user-detail-desc">{award.description}</p>
    </div>
  );
}
