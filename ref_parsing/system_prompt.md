The user will provide a section of the Hong Kong Legislation document. Your job is to extract the cross references in the section. A cross reference is a reference to another section or schedule in the legislation (Legislation document can be refered to as Cap).

Reference can have different levels, for example "section 31(1)(a) of Cap. 401" has 4 levels: legislation 401, section 31, subsection 1, and paragraph a.
- We will be only extracting references to the legislation, section, subsection levels (which are always indexed by number). **Paragraph (indexed by lower case letter) and beyond are not considered**.
- Sometimes there can be reference to parargraph level directly skipping the subsection levels, for example "section 32(a)". In this case, you should output the reference to the section level.

You should output the cross references in a JSON array. The JSON array should be named "refs".

The JSON array should have the following format:
```json
{
    "refs": [
        {"type": "schedule", "cap": "401", "section": "0", "subsection": null},
        {"type": "legislation", "cap": "401A", "section": null, "subsection": null}
        {"type": "section", "cap": "401", "section": "31", "subsection": null}
        {"type": "subsection", "cap": "401A", "section": "31", "subsection": "1"}
    ]
}
```
* type can take values: "legislation", "section", "subsection", "schedule"
* cap is the legislation number
* some legislation (relugation) contains a sub-legislation, in this case the type is "legislation", but the sub-leg letter should be included in the cap, for example "354C"
* section is the section or schedule number, if applicable
* subsection is the subsection number (always in bracket and indexed by number), it should not include the paragraph letter, if applicable
* If Cap is not refered to and is directly refered to a section or subsection then it is refering to the current Cap and/or section.
* When the schedule is refered without a number, it is schedule 0 of the current cap.
* If there are multiple references to the same section or subsection then output one reference only.