// Shared wrapper for every section: an anchor id, a heading and the section content.
export default function Section({ id, title, children }) {
  return (
    <section id={id} className="section">
      <h2>{title}</h2>
      {children}
    </section>
  );
}
