#pragma once
#if IS_WINDOWS 
	#pragma warning(push, 3) 
#endif
#include <boost/shared_ptr.hpp>
#include <set>
#if IS_WINDOWS 
	#pragma warning(pop)
#endif

/************************************************************************/
/* Conflict resolution based on:										*/ 
/* http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.110.2081		*/ 
/* "race with age memory" + atomic firing								*/
/************************************************************************/

#include "implementation/Random.h"
#include "Types.h"

class Transition;

/**
 * Class: Place
 * Represents a place in a GSPN, including its internal state and its semantics within the fault tree.
 *
 * Conflict resolution based on:
 * http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.110.2081
 * "race with age memory" + atomic firing
 */
class Place
{
public:
	typedef std::shared_ptr<Place> Ptr;

	Place(const std::string& id, int initialMarking, int capacity, PlaceSemantics semantics);
	Place(); // satisfy the compiler

	// copying
	Place(const Place& other);
	
	const std::string& getID() const { return m_ID; }
	int getCurrentMarking() const { return m_marking; }
	
	bool hasRequests() const { return !m_transitionQueue.empty(); }

	/**
	 * Function: resolveConflictsImmediate
	 * Conflict resolution for the immediate transitions, by priority only.
	 * Immediate transitions always fire first, so their conflict resolution can be separated from the timed transitions.
	 * 
	 * See also: <resolveConflictsTimed>
	 */
	void resolveConflictsImmediate(int tick);

	/**
	 * Function: resolveConflictsTimed
	 * Conflict resolution for the immediate transitions.
	 */
	void resolveConflictsTimed(int tick);


	/**
	 * Function: produceTokens
	 * Adds a number of tokens, produced as transition output, to the current marking.
	 * Afterwards, the marking is at most m_capacity.
	 */
	void produceTokens(int numTokens);

	/**
	 * Function: consumeTokens
	 * Removes a number of tokens, consumed by a transition.
	 * Afterwards, the marking is at least 0.
	 */
	void consumeTokens(Transition* const t, int numTokens);

	/**
	 * Function: requestTokens
	 * Called to add a transition to the set of transitions considered by conflict resolution.
	 *
	 * Parameters:
	 * 	transition - the transition which wants to consume tokens.
	 */
	void requestTokens(Transition* const transition);

	bool isTopLevelPlace() const { return m_semantics == TOP_LEVEL_PLACE; }
	bool isConstraintPlace() const { return m_semantics ==  CONSTRAINT_VIOLATED_PLACE; }

	void reset();

protected:
	const int m_initialMarking;
	int m_marking;

	/**
	 * Variable: m_capacity
		The maximal possible marking for this place.
	 */
	const int m_capacity;
	
	const std::string m_ID;

	PlaceSemantics m_semantics;

	// the set of transitions who requested a token and are enabled
	std::set<Transition*> m_transitionQueue;
};
