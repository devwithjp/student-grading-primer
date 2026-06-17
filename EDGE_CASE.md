# Edge case: students without a mark

The primer says `mark` is optional when creating a student, so the backend accepts
requests that omit `mark` or send it as an empty value. In that case the student
is stored with `mark: null` rather than inventing a score such as `0`.

This keeps the student's record persistent without treating an unknown mark as a
failing mark. The `/stats` endpoint only includes integer marks in its `count`,
`average`, `min`, and `max` calculations, so unmarked students do not distort the
class statistics.
