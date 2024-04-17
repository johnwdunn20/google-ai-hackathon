# Improving Interopability in HealthCare Data
_Created for Google AI Hackathon 2024_

### Background & Problem
The current standard for exchanging healthcare data is [FHIR](https://www.hl7.org/fhir/), but health systems can be slow to adapt and often use an older version of FHIR or a predecessor to the FHIR standard such as HL7 v2 or v3. Additionally, the FHIR standard is purposefully vague in order to give flexibility to those using the standard.

As a result, consumers of healthcare data are challenged to create a standard data model that encompasses the unqiue data standards of different providers. Additionally, any standard data model is not static. As standards change so must the data model.

This type of problem exists in other healthcare domains, such as machine readable files of rates and contracts that providers and payers must publish and many other areas outside of healthcare. When there a significant number of data producers, true data standardization is rare.

### Solution
We prefer to solve data discrepancies upstream, at the data layer, so that application logic can be built upon a standard 