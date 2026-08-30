//! Pure Rust semantic core for XoX tri-state epistemic logic.
//!
//! This module contains zero dependencies on Python, PyO3, or runtime execution environments.

/// Canonical tri-state logical value.
#[derive(Copy, Clone, Eq, PartialEq, Hash, Debug)]
pub enum XoXValue {
    True,
    False,
    Unknown,
}

impl XoXValue {
    /// Strong Kleene unary NOT (~).
    #[inline]
    pub const fn not(self) -> Self {
        match self {
            Self::True => Self::False,
            Self::False => Self::True,
            Self::Unknown => Self::Unknown,
        }
    }

    /// Strong Kleene binary conjunction (AND) for already-evaluated operands.
    #[inline]
    pub const fn and(self, other: Self) -> Self {
        match (self, other) {
            (Self::False, _) | (_, Self::False) => Self::False,
            (Self::True, Self::True) => Self::True,
            (Self::True, Self::Unknown)
            | (Self::Unknown, Self::True)
            | (Self::Unknown, Self::Unknown) => Self::Unknown,
        }
    }

    /// Strong Kleene binary disjunction (OR) for already-evaluated operands.
    #[inline]
    pub const fn or(self, other: Self) -> Self {
        match (self, other) {
            (Self::True, _) | (_, Self::True) => Self::True,
            (Self::False, Self::False) => Self::False,
            (Self::False, Self::Unknown)
            | (Self::Unknown, Self::False)
            | (Self::Unknown, Self::Unknown) => Self::Unknown,
        }
    }

    /// Returns true if an AND expression with `self` as LHS short-circuits (i.e. self is False).
    #[inline]
    pub const fn should_short_circuit_and(self) -> bool {
        matches!(self, Self::False)
    }

    /// Returns true if an OR expression with `self` as LHS short-circuits (i.e. self is True).
    #[inline]
    pub const fn should_short_circuit_or(self) -> bool {
        matches!(self, Self::True)
    }
}
